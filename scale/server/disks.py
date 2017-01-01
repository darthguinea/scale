from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping

class Disks(object):
    def __init__(self):
        self.volumes = []

    def add(self, volume_size=8, device='/dev/xvda'):
        dev = BlockDeviceType()
        dev.size = volume_size
        dev.delete_on_termination = True
        volume = BlockDeviceMapping()

        volume[device] = dev

        self.volumes.append(volume)

    def get(self):
        return self.volumes
