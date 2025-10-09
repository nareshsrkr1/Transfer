commands:
  - export PYTHONPATH=$SRC_DIR:$SRC_DIR/src:$SRC_DIR/windowApp:$PYTHONPATH; cd $SRC_DIR/windowApp; python -m pytest -v

test:
  requires:
    - pytest
  commands:
    - export PYTHONPATH=$SRC_DIR:$SRC_DIR/src:$SRC_DIR/windowApp:$PYTHONPATH
    - echo "PYTHONPATH=$PYTHONPATH"
    - cd $SRC_DIR/windowApp
    - python -m pytest --ignore=testEnvironment --cov=. --cov-report xml:../xunit-reports/xunit-result-titan.xml
