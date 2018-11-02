{
    "targets": [
        {
            "target_name": "mem_ctl",
            "sources": ["index.cc"],
            "include_dirs": ["<!(node -e \"require('nan')\")"],
            "cflags": [
                "-fexceptions",
                "-fpermissive",
                "-fexceptions",
                "-pthread",
                "-Wunused-but-set-variable"
            ],
            "cflags_cc": [
                "-fexceptions",
                "-fpermissive",
                "-std=c++11",
                "-pthread",
                "-Wunused-but-set-variable"
            ],
            "OTHER_CFLAGS": [
                "-fexceptions",
                "-fpermissive",
                "-fexceptions",
                "-pthread",
                "-Wunused-but-set-variable"
            ]
        }
    ]
}