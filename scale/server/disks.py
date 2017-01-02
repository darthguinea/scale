class Disks(object):
    def __init__(self):
        self.volumes = []

    def add(self, name=None, volume_size=8, device='/dev/sda1'):
        params = {
            'DeviceName': device,
            'Ebs': {
                'VolumeSize': volume_size,
                'VolumeType': 'gp2',
            }
        }

        if name is not None:
            params['VirtualName'] = name

        self.volumes.append(params)

    def get(self):
        return self.volumes
