# Windows virtual display driver

This directory contains the BOLT+ IddCx driver layer.

Microsoft's Indirect Display Driver model is designed for displays that are not attached to a traditional GPU output. The Microsoft Windows Driver Samples repository provides the IddSample implementation and demonstrates monitor enumeration, mode handling, swap-chain assignment, and frame processing.

Reference:

- https://github.com/microsoft/Windows-driver-samples/tree/main/video/IndirectDisplay
- https://learn.microsoft.com/en-us/windows-hardware/drivers/display/indirect-display-driver-model-overview

## Design

The driver reports one virtual monitor:

**Sphero BOLT+ Monitor**

The target display is intentionally small. The BOLT+ physical LED matrix is 8x8, so the eventual driver can expose an 8x8 logical mode or a more practical scaled mode such as 80x80 while the bridge downsamples the desktop image to 8x8.

The driver must not directly use Python, GDI, OpenGL, or Vulkan. IddCx supplies desktop frames through DirectX surfaces; the driver can hand the resulting frame data to the bridge through an appropriate IPC mechanism.

## Current state

The Python side is usable for BLE discovery and passive protocol capture.

The C++ driver files in this directory are a starting point for integrating the project with Microsoft's current IddCx sample. They should be built with a matching WDK/SDK and tested on a development machine before installation.

A production driver requires proper INF metadata, signing, installation, device lifecycle handling, swap-chain processing, and robust IPC.
