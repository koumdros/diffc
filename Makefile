#
# Makefile for diffc
#
# $URL$
# $Id$
#

SRC_SCRIPT_DIR=./src/script
BIN_DIR=./bin/python2
BIN3_DIR=./bin/python3

build: clean
	cat ./docs/HEADER > ${BIN_DIR}/diffc
	cat ${SRC_SCRIPT_DIR}/diff_match_patch.py | grep -v '#!/usr/bin/python2.4' >> ${BIN_DIR}/diffc
	cat ${SRC_SCRIPT_DIR}/diffc.py | grep -v '#!/usr/bin/python2.4' | grep -v 'import diff_match_patch' >> ${BIN_DIR}/diffc
	chmod 755 ${BIN_DIR}/diffc

build_test: build
	cp ${BIN_DIR}/diffc ${BIN_DIR}/diffc.py
	cp ${SRC_SCRIPT_DIR}/diffc_test.py ${BIN_DIR}
	python2.4 ${BIN_DIR}/diffc_test.py

build3: clean3
	cat ./docs/HEADER > ${BIN3_DIR}/diffc
	cp ${SRC_SCRIPT_DIR}/diff_match_patch.py /tmp/diff_match_patch.py.tmp
	perl -i -pe 's#/ (\d)#// $$1#g' /tmp/diff_match_patch.py.tmp
	cat /tmp/diff_match_patch.py.tmp  | grep -v '#!/usr/bin/python2.4' >> ${BIN3_DIR}/diffc
	cat ${SRC_SCRIPT_DIR}/diffc.py | grep -v '#!/usr/bin/python2.4' | grep -v 'import diff_match_patch' >> ${BIN3_DIR}/diffc
	chmod 755 ${BIN3_DIR}/diffc

build3_test: build3
	cp ${BIN3_DIR}/diffc ${BIN3_DIR}/diffc.py
	cp ${SRC_SCRIPT_DIR}/diffc_test.py ${BIN3_DIR}
	python3 ${BIN3_DIR}/diffc_test.py

clean:
	rm -rf ${BIN_DIR}/*
	mkdir -p ${BIN_DIR}

clean3:
	rm -rf ${BIN3_DIR}/*
	mkdir -p ${BIN3_DIR}
	rm -f /tmp/diff_match_patch.py.tmp
