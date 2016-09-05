


# Refresh SENSU
# salt-run cache.clear_grains tgt="*" ; salt '*' state.sls sensu.client; salt '*' service.restart salt-minion; salt '*' mine.flush; salt '*' mine.update ; salt 'mon01*' state.sls sensu


@roles('ntw')
def clean_contrail():
    sudo(uptime)
    sudo(hostname)

