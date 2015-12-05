import os
import uuid
import git


class Repo(object):
    __repo_config__ = {}
    r_version = 0
    r_uuid = None
    r_annexes = []

    def __init__(self, basepath):
        self._basepath = basepath

    def init(self):
        try:
            repo = git.Repo(self._basepath)
        except git.InvalidGitRepositoryError:
            repo = git.Repo.init(self._basepath, bare=False)
        cfg = repo.config_writer()

        if not cfg.has_section('annex'):
            cfg.add_section('annex')

        if not cfg.has_option('annex', 'uuid'):
            cfg.set('annex', 'uuid', uuid.uuid4())

        if not cfg.has_option('annex', 'version'):
            cfg.set('annex', 'version', 5)

        cfg.release()

        paths = ['objects', 'tmp', 'misctmp', 'bad', 'transfers', 'ssh',
                 'journal']

        annex_path = os.path.join(self._basepath, '.git/annex')
        for path in paths:
            tmp = os.path.join(annex_path, path)
            if not os.path.exists(tmp):
                os.makedirs(tmp)

    def config_reader(self):
        repo = git.Repo(self._basepath)
        cfg = repo.config_reader()
        for section in cfg.sections():
            self.__repo_config__[section] = {}
            for option in cfg.options(section):
                self.__repo_config__[section][option] = cfg.get(section,
                                                                option)

        self.r_version = int(self.__repo_config__['annex']['version'])
        self.r_uuid = uuid.UUID(self.__repo_config__['annex']['uuid'])
