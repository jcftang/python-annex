import py
import pytest
import os
import uuid
import git
import annex.repo
from annex.key import Key

FIXTURE_DIR = py.path.local(
		os.path.dirname(
			os.path.realpath(__file__)
			)
		) / '_fixture_files'

def test_repo(tmpdir):
    repo = annex.repo.Repo(tmpdir.dirname)
    repo.init()
    assert os.path.exists(os.path.join(tmpdir.dirname, '.git/annex'))

    cfg = repo.config_reader()
    assert 'annex' in repo.__repo_config__
    assert isinstance(repo.r_uuid, uuid.UUID)
    assert repo.r_version == 5


def test_keyname(tmpdir):
    key = Key()
    data = 'foobar'
    key.create(data)
    assert key.g_backend == 'sha256'.upper()
    assert key.g_name == 'c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'
    assert key.keyname(
    ) == 'SHA256-s6--c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'


def test_keypath():
    key = Key()
    keyname = 'SHA256-s6--c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2'
    key.keypath(keyname)
    assert key.keypath(keyname) == '11d/8ca/'


@pytest.mark.datafiles(
		FIXTURE_DIR / 'uuid.log',
		on_duplicate='ignore',
		)
def test_log(datafiles):
    from annex.log import Annex, UUIDLog
    import schematics.models
    a = Annex()
    with pytest.raises(schematics.models.ModelValidationError):
        a.validate()

    uuidlogfile = datafiles.join('uuid.log')
    u = UUIDLog()
    annexes = []
    for line in uuidlogfile.open():
	a = Annex()
        a.id, a.desc, a.timestamp = u.parseline(line)
        assert a.validate() == None
	annexes.append(a)
    assert len(annexes) == 2
    assert annexes[0] != annexes[1]

    new_u = UUIDLog()
    annexes = new_u.parselog(str(uuidlogfile))
    assert len(annexes) == 2
