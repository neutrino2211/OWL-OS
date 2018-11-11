def make_dirs(p):
    # if not exists("/".join(p.split("/")[:1])) :
        # raise OWLPathError(p)
    # m = json.loads(open("./storage/storagemap.json").read())
    counts = {}
    parts = p.split('/')
    branch = counts
    for part in parts:
        branch = branch.setdefault(part, {})
    print(counts,branch)
make_dirs("a/b/c")