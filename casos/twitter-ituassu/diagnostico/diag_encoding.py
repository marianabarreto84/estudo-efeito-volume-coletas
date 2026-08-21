"""Diagnostico de encoding da tabela ituassu_2014."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # raiz do projeto no sys.path
from core.db import conectar

with conectar(vm="vm067", dbname="eTC_Producao") as conn:
    cur = conn.cursor()
    print("server_encoding:", end=" ")
    cur.execute("SHOW server_encoding;"); print(cur.fetchone()[0])
    print("client_encoding (default):", end=" ")
    cur.execute("SHOW client_encoding;"); print(cur.fetchone()[0])

    # Pega hashtags que contem 'elei' e mostra bytes crus (via convert_to em cada encoding candidato)
    print("\n== bytes crus de hashtags com 'elei' (primeiras distintas) ==")
    cur.execute("""
        SELECT DISTINCT lower(tag)
        FROM (SELECT hashtags FROM ituassu_2014 WHERE cardinality(hashtags)>0 LIMIT 300000) s,
             LATERAL unnest(s.hashtags) tag
        WHERE lower(tag) LIKE 'elei%2014'
        LIMIT 10;""")
    tags = [r[0] for r in cur.fetchall()]
    for t in tags:
        # t ja e str Python (decodificado pelo client_encoding). Mostra codepoints.
        print(f"  str={t!r}")
        print(f"    codepoints={[hex(ord(c)) for c in t]}")

    # Agora testa reinterpretacao: pega o mesmo dado como bytea sob diferentes convert_to
    print("\n== reinterpretacao de um hashtag 'eleicoes2014' acentuado ==")
    cur.execute("""
        SELECT tag,
               encode(convert_to(tag,'UTF8'),'hex')   AS as_utf8,
               encode(convert_to(tag,'LATIN1'),'hex')  AS as_latin1
        FROM (SELECT hashtags FROM ituassu_2014 WHERE cardinality(hashtags)>0 LIMIT 300000) s,
             LATERAL unnest(s.hashtags) tag
        WHERE lower(tag) LIKE 'elei%2014' AND tag !~ '^[[:ascii:]]+$'
        LIMIT 3;""")
    for r in cur.fetchall():
        print(f"  tag={r[0]!r}")
        print(f"    convert_to UTF8  (hex)={r[1]}")
        print(f"    convert_to LATIN1(hex)={r[2]}")
    cur.close()

# Segunda conexao: forcar client_encoding=LATIN1 e ver se renderiza certo
print("\n== mesma consulta com client_encoding=LATIN1 ==")
with conectar(vm="vm067", dbname="eTC_Producao", local_port=5456) as conn:
    conn.set_client_encoding("LATIN1")
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT tag
        FROM (SELECT hashtags FROM ituassu_2014 WHERE cardinality(hashtags)>0 LIMIT 300000) s,
             LATERAL unnest(s.hashtags) tag
        WHERE lower(tag) LIKE 'elei%2014' AND tag !~ '^[[:ascii:]]+$'
        LIMIT 5;""")
    for r in cur.fetchall():
        print(f"  {r[0]!r}")
    cur.close()
