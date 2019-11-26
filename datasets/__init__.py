from .urisc import UriscEdgeDetection

datasets = {
    'urisc': UriscEdgeDetection,
}

def get_dataset(name, **kwargs):
    return datasets[name.lower()](**kwargs)