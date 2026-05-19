# OpenNI2 Python 3 Bindings 

This package contains the OpenNI Python bindings written by Séverin Lemaignan updated for modern Python 3.8+.

## Quick Start

### Installation
```bash
# Navigate to the project
cd openni-python3

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Basic Usage
```python
from openni import openni2

# Initialize OpenNI2
openni2.initialize()

# Use normally
device = openni2.Device.open_any()
print(device.get_device_info())

# Cleanup
openni2.unload()
```

## Related Links

- **Original Project**: https://github.com/severin-lemaignan/openni-python


## 📄 License

MIT License - See [openni-python3/LICENSE](openni-python3/LICENSE)
