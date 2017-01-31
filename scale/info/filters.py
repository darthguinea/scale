class Filters(object):

	def __new__(self,
					name=None,
					instance_type=None,
					state=None,
					tags=[],
					):

		filters = []

		if state is not None:
			filters.append({'Name': 'instance-state-name', 'Values': [state]})

		if instance_type is not None:
			filters.append({'Name': 'instance-type', 'Values': [instance_type]})

		if len(tags) > 0:
			for tag in tags:
				filters.append({
								'Name': '{0}:{1}'.format('tag', tag['Key']),
								'Values': [tag['Value']]
								})
		
		return filters
