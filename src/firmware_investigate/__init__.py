"""Firmware investigation toolkit for motorcycle headset firmware."""

__version__ = "0.1.0"

from .usb_gadget import USBGadgetFaker, SENA_DEVICE, CARDO_DEVICE

__all__ = ["__version__", "USBGadgetFaker", "SENA_DEVICE", "CARDO_DEVICE"]
