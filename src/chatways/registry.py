class Registry(dict):
    def __init__(self, module_name, registry_map):
        super().__init__()
        self.module_name = module_name
        self.registry_map = registry_map

    def _import_from_register(self, key):
        value = self.registry_map[key]
        exec(f"from chatways.{self.module_name}.{key} import {value}")

    def _import_key(self, key):
        try:
            self._import_from_register(key)
        except Exception as e:
            print(f"import {key} failed, details: {e}")

    def __getitem__(self, key):
        if key not in self.keys():
            self._import_key(key)
        return super().__getitem__(key)

    def __contains__(self, key):
        self._import_key(key)
        return super().__contains__(key)
