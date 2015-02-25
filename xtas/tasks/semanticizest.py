from xtas.core import app
from xtas.tasks import tokenize
from semanticizest import Semanticizer
from semanticizest.parse_wikidump import Db, parse_dump, DUMP_TEMPLATE

from .._downloader import _make_data_home, _progress


MODEL = {}
# Read in all models that we have 
home = _make_data_home()
sem_dir = os.path.join(home, 'semanticizest')
for model in os.glob.glob(os.path.join(sem_dir, "*.model")):
    lang, _ = os.path.splitext(model)
    MODEL[lang] = Semanticizer(lang+'wiki.model')


def download(lang):
    home = _make_data_home()
    sem_dir = os.path.join(home, 'semanticizest')
    
    url = DUMP_TEMPLATE.format(lang + "wiki")
    local_fname = os.path.join(sem_dir, lang + "wiki.xml.bz2")
    if not os.path.exists(sem_dir):
        logger.info('Downloading latest Wikipedia snapshot for %s' % lang)
        urlretrieve(url, local_fname, reporthook=_progress)

    return local_fname


@app.task
def semanticize(doc, lang="en"):
    global MODEL
    if not lang.isalpha():
        raise ValueError("not a valid language: %r" % lang)
    if lang not in MODEL:
        try:
            MODEL[lang] = Semanticizer(lang+'wiki.model')
        except Exception as e:
            try:
                local_fname = download(lang)
                # Init, connect to DB and setup db schema
                db = Db(lang + "wiki.model")
                db.connect()
                db.setup()
                # Parse wiki snapshot and store it to DB
                parse_dump(local_fname, db.db)
                # Close connection to DB and exit
                db.disconnect()
            except Exception as e:
                print "ERROR downloading and/or parsing Wikipedia snapshot for [%s]: %s" % (lang, e)
                raise
    text = fetch(doc)
    return MODEL[lang].all_candidates(tokenize(text))

