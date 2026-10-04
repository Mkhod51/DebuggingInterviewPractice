"""Standard-library tests; run with python3 -m unittest discover -s scripts."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('helper', Path(__file__).with_name('start_attempt.py'))
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class AttemptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'projects/easy/e01-example'
        self.project.mkdir(parents=True)
        (self.project / 'pyproject.toml').write_text('[project]\n')
        (self.project / 'README.md').write_text('contract')
        (self.project / 'src').mkdir()
        (self.project / 'src/app.py').write_text('value = 1\n')

    def test_copy_preserves_source_and_excludes_generated_files(self):
        for name in ['.venv', '__pycache__', 'build', 'dist', 'app.egg-info']:
            (self.project / name).mkdir()
            (self.project / name / 'generated').write_text('ignore')
        destination = helper.start_attempt('e01', 'first', self.root)
        self.assertEqual((destination / 'src/app.py').read_text(), 'value = 1\n')
        self.assertEqual(sorted(p.name for p in destination.iterdir()), ['README.md', 'pyproject.toml', 'src'])
        (destination / 'src/app.py').write_text('changed')
        self.assertEqual((self.project / 'src/app.py').read_text(), 'value = 1\n')

    def test_collision_preserves_previous_work(self):
        first = helper.start_attempt('E01', 'first', self.root)
        (first / 'README.md').write_text('my work')
        with self.assertRaises(FileExistsError):
            helper.start_attempt('E01', 'first', self.root)
        second = helper.start_attempt('E01', 'second', self.root)
        self.assertEqual((first / 'README.md').read_text(), 'my work')
        self.assertNotEqual(first, second)

    def test_unknown_ids_and_path_traversal_are_rejected(self):
        for project_id in ['E00', 'H06', '../E01', 'M01']:
            with self.subTest(project_id=project_id), self.assertRaises(ValueError):
                helper.start_attempt(project_id, 'safe', self.root)
        with self.assertRaises(ValueError):
            helper.start_attempt('E01', '../escape', self.root)
        self.assertFalse((self.root / 'attempts').exists())

    def test_cli_is_independent_of_callers_working_directory(self):
        scripts = self.root / 'scripts'
        scripts.mkdir()
        target = scripts / 'start_attempt.py'
        target.write_text(Path(helper.__file__).read_text())
        result = subprocess.run([sys.executable, str(target), 'E01', '--name', 'cli'],
                                cwd='/', text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'attempts/e01-cli/src/app.py').is_file())
        self.assertIn('python -m pytest -q', result.stdout)


if __name__ == '__main__':
    unittest.main()
