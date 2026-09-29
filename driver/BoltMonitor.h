#pragma once

#include <wdf.h>
#include <iddcx.h>

class BoltMonitorDevice
{
public:
    explicit BoltMonitorDevice(WDFDEVICE device);
    ~BoltMonitorDevice();

    NTSTATUS Initialize();

private:
    WDFDEVICE m_device;
    IDDCX_ADAPTER m_adapter{};
};
