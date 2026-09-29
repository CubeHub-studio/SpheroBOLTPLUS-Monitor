from bridge.bolt_protocol import (
    EOP,
    SOP,
    build_sphero_command,
    sphero_checksum,
)


def main() -> None:
    packet = build_sphero_command(
        device_id=0x1A,
        command_id=0x2D,
        payload=[0x8D, 0xD8, 0xAB, 0x00, 0xFF],
        sequence=1,
    )

    assert packet[0] == SOP
    assert packet[-1] == EOP

    print("Sphero V2 packet framing: OK")
    print("Escaped packet:")
    print(packet.hex(" "))

    body = [0x0A, 0x1A, 0x2D, 0x01, 0x8D, 0xD8, 0xAB, 0x00, 0xFF]
    print(f"Checksum example: 0x{sphero_checksum(body):02X}")
    print()
    print("This test does NOT connect to or write to the BOLT+.")


if __name__ == "__main__":
    main()
