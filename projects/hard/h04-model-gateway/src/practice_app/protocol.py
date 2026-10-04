"""Transport encoding and correlated response validation."""
from copy import deepcopy


class ProtocolError(ValueError):
    pass


def encode(request, model):
    return dict(request_id=model, model=model, text=request.text,
                options=deepcopy(request.options))


def decode(request, model, response):
    if not isinstance(response, dict):
        raise ProtocolError("Response must be an object")
    if response.get("request_id") != request.request_id:
        raise ProtocolError("Response correlation mismatch")
    if response.get("model") != model:
        raise ProtocolError("Response model mismatch")
    output = response.get("output") or None
    if not isinstance(output, str):
        raise ProtocolError("Output must be a string")
    return output


def validate_call(body):
    if set(body) != {"request_id", "model", "text", "options"}:
        raise ProtocolError("Malformed call body")
    if not isinstance(body["options"], dict):
        raise ProtocolError("Malformed call options")
