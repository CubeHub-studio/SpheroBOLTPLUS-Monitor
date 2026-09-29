#include "BoltMonitor.h"

BoltMonitorDevice::BoltMonitorDevice(WDFDEVICE device)
    : m_device(device)
{
}

BoltMonitorDevice::~BoltMonitorDevice()
{
}

NTSTATUS BoltMonitorDevice::Initialize()
{
    // The complete production implementation should be based on the current
    // Microsoft IddSampleDriver and customized for the BOLT+ endpoint.
    //
    // Keeping this adapter initialization isolated makes it possible to add
    // swap-chain processing and IPC without mixing those concerns with BLE.

    IDDCX_ADAPTER_CAPS caps{};
    caps.Size = sizeof(caps);
    caps.MaxMonitorsSupported = 1;

    caps.EndPointDiagnostics.Size = sizeof(caps.EndPointDiagnostics);
    caps.EndPointDiagnostics.pEndPointFriendlyName = L"Sphero BOLT+ Monitor";
    caps.EndPointDiagnostics.pEndPointManufacturerName = L"CubeHub-studio";
    caps.EndPointDiagnostics.pEndPointModelName = L"BOLT+ 8x8";

    return STATUS_NOT_IMPLEMENTED;
}
