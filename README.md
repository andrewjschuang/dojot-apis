# dojot-apis
api endpoints for dojot

## Requirements
```bash
python3 -m venv ve
source ve/bin/activate
pip install requests
```

## Usage
```python
import rest
from pprint import pprint
jwt = rest.login()
pprint(rest.get_devices(jwt))
```
