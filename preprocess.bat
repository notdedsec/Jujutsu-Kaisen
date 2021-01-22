@echo off

for %%A in (*.mkv) do (
    echo Processing %%A
    py preprocess.py "%%A"
    del "%%A.ass"
)

for %%A in (*.ass) do (
    echo Processing %%A
    py preprocess.py "%%A"
    del "%%A"
)

@pause