
from collections import OrderedDict
from .constants import INITIATED, ACTED, TRACKED


def validate_request(data):

    if not data.get('type'):
        return False
    else:
        block_type = data['type']
        if block_type == INITIATED:
            return validate_initiated_request(data)
        elif block_type == ACTED:
            return validate_acted_request(data)
        elif block_type == TRACKED:
            return validate_tracked_request(data)
        else:
            return False


def validate_initiated_request(data):
    required = ['actor', 'supplier', 'item', 'quantity', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'actor': data['actor'],
        'supplier': data['supplier'],
        'item': data['item'],
        'quantity': data['quantity']
    })


def validate_acted_request(data):
    required = ['node_id', 'actor', 'origin', 'destination', 'item', 'quantity', 'action', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'actor': data['actor'],
        'origin': data['origin'],
        'destination': data['destination'],
        'item': data['item'],
        'action': data['action'],
        'quantity': data['quantity']
    })


def validate_tracked_request(data):
    required = ['node_id', 'actor', 'courier', 'status', 'signature']
    if not all(k in data for k in required):
        return False

    return OrderedDict({
        'actor': data['actor'],
        'courier': data['courier'],
        'status': data['status']
    })
