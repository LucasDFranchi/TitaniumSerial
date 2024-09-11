from proto import CommunicationProtobuf

def transmit_protobuf():
    cp = CommunicationProtobuf()
    
    cp.update_command(1)
    cp.update_address(0x1510)
    cp.update_memory_area(4)
    cp.update_recv_memory_area(72)
    cp.update_payload("This is just a test!")
    
    
    output_buffer = bytearray([0x00] * 256)
    print(len(output_buffer))
    cp.serialize(output_buffer)
    
    print(output_buffer)
    
transmit_protobuf()