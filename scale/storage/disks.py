class Disks(object):
    def __init__(self):
        self.volumes = []

    def add(self, name=None, volume_size=8, 
                device='/dev/sda1', encrypted=False,
                volume_type='gp2', iops=100):

        params = {
            'VirtualName': name,
            'DeviceName': device,
            'Ebs': {
                'VolumeSize': volume_size,
                'VolumeType': volume_type,
                'Encrypted': encyrpted
            }
        }

        if name is not None:
            params['VirtualName'] = name

        if volume_type is 'io1':
            params['Iops'] = iops

        self.volumes.append(params)

    def get(self):
        return self.volumes
