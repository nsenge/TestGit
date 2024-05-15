load("@pyoxidizer//py/crates:crates.bzl", "project")
load("@pyoxidizer//py/crates:crates.bzl", "source_crates")

project(
    name = "MonProjet",
    version = "1.0.0",
    description = "Description de votre projet",
)

binary(
    name = "mon_projet",
    path = "mon_projet",
    entry_point = "ProjetBDD:mainloop",  # Assurez-vous que c'est le bon point d'entrée pour votre application
)

source_crates = {
    "my_project": {
        "path": ".",
        "binaries": [
            "mon_projet",
        ],
    },
}

dependencies = [
    "@pip_mysql_connector_python//:*",  # Dépendance MySQL-Connector-Python
    "@pip_pymysql//:*",  # Dépendance PyMySQL
]