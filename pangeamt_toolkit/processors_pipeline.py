import yaml as _yaml

class Pipeline:
    def __init__(self, processors, processors_config):
        """ processors is a list of dicts from the general config file
            with this structure:
                {
                    'name': processor's shortname,
                    'args': [list of the processor's args]
                }

            processors_config is a path to a yaml file that contains a
            dict with this structure:
                {
                    'processor's shortname': {
                        'class': 'processor's class name',
                        'path': 'processor's path'
                    }
                }
        """
        with open(processors_config, 'r') as file:
            self._config = _yaml.safe_load(file)
        self._processes = []
        for process in processors:
            processor = self._config[process['name']]
            klass_name = processor['class']
            path = processor['path']
            args = process['args']
            mod = __import__(path, fromlist=[klass_name])
            klass = getattr(mod, klass_name)
            processor = klass(*args)
            self._processes.append(processor)

    def preprocess(self, seg):
        for process in self._processes:
            process.preprocess(seg)

    def postprocess(self, seg):
        processes = self._processes[::-1]
        for process in processes:
            process.postprocess(seg)
