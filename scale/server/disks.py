from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping

class Disks(object):

    def __init__(self):
        self.volumes = []

    def create_disk(self, volume_size=8, device='/dev/xvda'):
        dev = BlockDeviceType()
        dev.size = volume_size
        dev.delete_on_termination = True
        volume = BlockDeviceMapping()

        volume[device] = dev

        self.volumes.append(volume)

    def disks(self):
        return self.volumes
