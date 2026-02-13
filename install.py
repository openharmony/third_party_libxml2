#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import subprocess
import sys


def untar_file(tar_file_path, extract_path, args):
    try:
        if os.path.exists(extract_path):
            rm_cmd = ['rm', '-rf', extract_path]
            subprocess.run(rm_cmd, check=True)

        tar_cmd = ['tar', '-xvf', tar_file_path, '-C', args.gen_dir]
        subprocess.run(tar_cmd, check=True)

    except Exception as e:
        print("tar error!")
        return


def apply_patch(patch_file, target_dir):
    try:
        if not os.path.exists(target_dir):
            return

        patch_cmd = ['patch', '-p1', "--fuzz=0", "--no-backup-if-mismatch", '-i', patch_file, '-d', target_dir]
        subprocess.run(patch_cmd, check=True)

    except Exception as e:
        print("apply_patch error!")
        return


def do_patch(args, target_dir):
    patch_file = [
        "Fix-memleaks-in-xmlXIncludeProcessFlags.patch",
        "backport-parser-Fix-potential-memory-leak-in-xmlParseAttValue.patch",
        "Fix-memory-leaks-for-xmlACatalogAdd.patch",
        "Fix-memory-leaks-in-xmlACatalogAdd-when-xmlHashAddEntry-failed.patch",
        "backport-CVE-2022-40303-Fix-integer-overflows-with-XML_PARSE_.patch",
        "backport-CVE-2022-40304-Fix-dict-corruption-caused-by-entity-.patch",
        "backport-schemas-Fix-null-pointer-deref-in-xmlSchemaCheckCOSS.patch",
        "libxml2-multilib.patch",
        "Fix-CVE-2023-25062.patch",
        "Fix-CVE-2023-45322-pre.patch",
        "Fix-CVE-2023-45322-first.patch",
        "Fix-CVE-2023-45322-second.patch",
        "backport-Add-whitespace-folding-for-some-atomic-data-types-th.patch",
        "backport-Properly-fold-whitespace-around-the-QName-value-when.patch",
        "backport-Avoid-arithmetic-on-freed-pointers.patch",
        "backport-fix-xmlXPathParserContext-could-be-double-delete-in-.patch",
        "backport-Use-UPDATE_COMPAT-consistently-in-buf.c.patch",
        "backport-Restore-behavior-of-htmlDocContentDumpFormatOutput.patch",
        "backport-Fix-use-after-free-bugs-when-calling-xmlTextReaderCl.patch",
        "backport-Use-xmlNewDocText-in-xmlXIncludeCopyRange.patch",
        "backport-xmlBufAvail-should-return-length-without-including-a.patch",
        "backport-Fix-integer-overflow-in-xmlBufferDump.patch",
        "backport-Fix-missing-NUL-terminators-in-xmlBuf-and-xmlBuffer-.patch",
        "backport-Reserve-byte-for-NUL-terminator-and-report-errors-co.patch",
        "backport-Fix-unintended-fall-through-in-xmlNodeAddContentLen.patch",
        "backport-Don-t-reset-nsDef-when-changing-node-content.patch",
        "backport-Avoid-double-free-if-malloc-fails-in-inputPush.patch",
        "backport-Fix-memory-leak-in-xmlLoadEntityContent-error-path.patch",
        "backport-Reset-nsNr-in-xmlCtxtReset.patch",
        "backport-Fix-htmlReadMemory-mixing-up-XML-and-HTML-functions.patch",
        "backport-Don-t-initialize-SAX-handler-in-htmlReadMemory.patch",
        "backport-Fix-HTML-parser-with-threads-and-without-legacy.patch",
        "backport-Fix-xmlCtxtReadDoc-with-encoding.patch",
        "backport-Use-xmlStrlen-in-CtxtReadDoc.patch",
        "backport-Create-stream-with-buffer-in-xmlNewStringInputStream.patch",
        "backport-Use-xmlStrlen-in-xmlNewStringInputStream.patch",
        "backport-Fix-memory-leak-with-invalid-XSD.patch",
        "backport-Make-XPath-depth-check-work-with-recursive-invocatio.patch",
        "backport-Fix-overflow-check-in-SAX2.c.patch",
        "backport-xinclude-Fix-memory-leak-when-fuzzing.patch",
        "backport-xinclude-Fix-more-memory-leaks-in-xmlXIncludeLoadDoc.patch",
        "backport-schemas-Fix-infinite-loop-in-xmlSchemaCheckElemSubst.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlCreatePushParserCt.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlNewPropInternal.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlNewDocNodeEatName.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-xmlSkipBlankChars.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSAX2ExternalSubset.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlParseReference.patch",
        "backport-malloc-fail-Fix-use-after-free-in-xmlXIncludeAddNode.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlStringGetNodeList.patch",
        "backport-parser-Fix-error-message-in-xmlParseCommentComplex.patch",
        "backport-io-Fix-buffer-full-error-with-certain-buffer-sizes.patch",
        "backport-reader-Switch-to-xmlParserInputBufferCreateMem.patch",
        "backport-uri-Allow-port-without-host.patch",
        "backport-parser-Fix-consumed-accounting-when-switching-encodi.patch",
        "backport-html-Fix-check-for-end-of-comment-in-push-parser.patch",
        "backport-parser-Fix-push-parser-with-1-3-byte-initial-chunk.patch",
        "backport-parser-Restore-parser-state-in-xmlParseCDSect.patch",
        "backport-parser-Remove-dangerous-check-in-xmlParseCharData.patch",
        "backport-parser-Don-t-call-DefaultSAXHandlerInit-from-xmlInit.patch",
        "backport-Correctly-relocate-internal-pointers-after-realloc.patch",
        "backport-Avoid-creating-an-out-of-bounds-pointer-by-rewriting.patch",
        "backport-error-Make-sure-that-error-messages-are-valid-UTF-8.patch",
        "backport-io-Check-for-memory-buffer-early-in-xmlParserInputGrow.patch",
        "backport-io-Remove-xmlInputReadCallbackNop.patch",
        "backport-Revert-uri-Allow-port-without-host.patch",
        "backport-xmlParseStartTag2-contains-typo-when-checking-for-default.patch",
        "backport-parser-Fix-integer-overflow-of-input-ID.patch",
        "backport-parser-Don-t-increase-depth-twice-when-parsing-internal.patch",
        "backport-xpath-number-should-return-NaN.patch",
        "backport-error-Don-t-move-past-current-position.patch",
        "backport-malloc-fail-Handle-memory-errors-in-xmlTextReaderEntPush.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-xmlParseTextDecl.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlAddDefAttrs.patch",
        "backport-malloc-fail-Fix-null-deref-if-growing-input-buffer-fails.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlSAX2AttributeInternal.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlBufResize.patch",
        "backport-buf-Fix-return-value-of-xmlBufGetInputBase.patch",
        "backport-malloc-fail-Don-t-call-xmlErrMemory-in-xmlstring.c.patch",
        "backport-malloc-fail-Fix-reallocation-in-inputPush.patch",
        "backport-malloc-fail-Fix-use-after-free-in-xmlParseStartTag2.patch",
        "backport-malloc-fail-Add-error-checks-in-xmlXPathEqualValuesCommon.patch",
        "backport-malloc-fail-Add-error-check-in-xmlXPathEqualNodeSetFloat.patch",
        "backport-malloc-fail-Fix-error-check-in-xmlXPathCompareValues.patch",
        "backport-malloc-fail-Record-malloc-failure-in-xmlXPathCompLiteral.patch",
        "backport-malloc-fail-Check-return-value-of-xmlXPathNodeSetDupNs.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlXIncludeLoadTxt.patch",
        "backport-malloc-fail-Fix-reallocation-in-xmlXIncludeNewRef.patch",
        "backport-xinclude-Fix-quadratic-behavior-in-xmlXIncludeLoadTx.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlParserInputBufferCreateMem.patch",
        "backport-malloc-fail-Check-for-malloc-failure-in-xmlFindCharEncodingHandler.patch",
        "backport-malloc-fail-Fix-leak-of-xmlCharEncodingHandler.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlParseEntityDecl.patch",
        "backport-encoding-Cast-toupper-argument-to-unsigned-char.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathCompareValues.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathTryStreamCompile.patch",
        "backport-malloc-fail-Fix-memory-leak-after-calling-valuePush.patch",
        "backport-malloc-fail-Fix-memory-leak-after-calling-xmlXPathWrapNodeSet.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXIncludeAddNode.patch",
        "backport-malloc-fail-Fix-memory-leak-after-xmlRegNewState.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSAX2StartElementNs.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlGetDtdElementDesc2.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlDocDumpFormatMemoryEnc.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-htmlParseStartTag1.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXIncludeLoadTxt.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlCopyPropList.patch",
        "backport-malloc-fail-Fix-memory-leak-after-calling-xmlXPathNodeSetMerge.patch",
        "backport-malloc-fail-Fix-memory-leak-after-calling-xmlXPathWrapString.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathEqualValuesCommon.patch",
        "backport-malloc-fail-Fix-memory-leak-in-htmlCreateMemoryParserCtxt.patch",
        "backport-malloc-fail-Fix-memory-leak-in-htmlCreatePushParserCtxt.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-htmlParseContentInternal.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-htmlParseStartTag2.patch",
        "backport-malloc-fail-Fix-null-deref-in-htmlnamePush.patch",
        "backport-malloc-fail-Fix-infinite-loop-in-htmlParseDocTypeDecl.patch",
        "backport-malloc-fail-Fix-error-code-in-htmlParseChunk.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlFAParseCharProp.patch",
        "backport-malloc-fail-Fix-leak-of-xmlRegAtom.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlRegexpCompile.patch",
        "backport-malloc-fail-Fix-OOB-read-after-xmlRegGetCounter.patch",
        "backport-parser-Fix-OOB-read-when-formatting-error-message.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathEqualNodeSetF.patch",
        "backport-malloc-fail-Fix-use-after-free-related-to-xmlXPathNo.patch",
        "backport-regexp-Add-sanity-check-in-xmlRegCalloc2.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlXPathCompiledEvalIn.patch",
        "backport-malloc-fail-Fix-null-deref-after-xmlPointerListAddSi.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlGetNsList.patch",
        "backport-malloc-fail-Check-for-malloc-failure-in-xmlHashAddEn.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathCacheNewNodeS.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathDistinctSorte.patch",
        "backport-xpath-Fix-harmless-integer-overflow-in-xmlXPathTrans.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathNameFunction.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSchemaItemListAddS.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlGet-Min-Max-Occurs.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlSchemaValAtomicType.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlSchemaInitTypes.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSchemaParse.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlCopyNamespaceList.patch",
        "backport-malloc-fail-Fix-another-memory-leak-in-xmlSchemaBuck.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlSchemaParseUnion.patch",
        "backport-malloc-fail-Fix-memory-leak-in-WXS_ADD_-LOCAL-GLOBAL.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSchemaBucketCreate.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlSchemaParseWildcard.patch",
        "backport-malloc-fail-Fix-type-confusion-after-xmlSchemaFixupT.patch",
        "backport-malloc-fail-Fix-null-deref-after-xmlSchemaItemList-A.patch",
        "backport-malloc-fail-Fix-null-deref-after-xmlSchemaCompareDat.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlSchemaParseUnion.patch",
        "backport-malloc-fail-Fix-memory-leak-in-xmlXPathRegisterNs.patch",
        "backport-catalog-Fix-memory-leaks.patch",
        "backport-CVE-2023-29469.patch",
        "backport-CVE-2023-28484.patch",
        "backport-valid-Allow-xmlFreeValidCtxt-NULL.patch",
        "backport-parser-Use-size_t-when-subtracting-input-buffer-poin.patch",
        "backport-malloc-fail-Fix-null-deref-in-xmlParserInputShrink.patch",
        "backport-xmllint-Fix-memory-leak-with-pattern-stream.patch",
        "backport-xzlib-Fix-implicit-sign-change-in-xz_open.patch",
        "backport-html-Fix-quadratic-behavior-in-htmlParseTryOrFinish.patch",
        "backport-valid-Make-xmlValidateElement-non-recursive.patch",
        "backport-malloc-fail-Fix-buffer-overread-in-htmlParseScript.patch",
        "backport-malloc-fail-Add-more-error-checks-when-parsing-names.patch",
        "backport-malloc-fail-Add-error-check-in-htmlParseHTMLAttribut.patch",
        "backport-parser-Limit-name-length-in-xmlParseEncName.patch",
        "backport-encoding-Fix-error-code-in-asciiToUTF8.patch",
        "backport-malloc-fail-Fix-buffer-overread-with-HTML-doctype-de.patch",
        "backport-parser-Fix-regression-in-xmlParserNodeInfo-accountin.patch",
        "backport-regexp-Fix-cycle-check-in-xmlFAReduceEpsilonTransiti.patch",
        "backport-regexp-Fix-checks-for-eliminated-transitions.patch",
        "backport-regexp-Fix-determinism-checks.patch",
        "backport-regexp-Fix-mistake-in-previous-commit.patch",
        "backport-regexp-Fix-null-deref-in-xmlFAFinishReduceEpsilonTra.patch",
        "backport-hash-Fix-possible-startup-crash-with-old-libxslt-ver.patch",
        "backport-parser-Fix-old-SAX1-parser-with-custom-callbacks.patch",
        "backport-xmllint-Fix-use-after-free-with-maxmem.patch",
        "backport-malloc-fail-Check-for-malloc-failures-when-creating.patch",
        "backport-malloc-fail-Fix-buffer-overread-after-htmlParseScrip.patch",
        "backport-xmlValidatePopElement-can-return-invalid-value-1.patch",
        "backport-Fix-use-after-free-in-xmlParseContentInternal.patch",
        "backport-malloc-fail-Fix-null-deref-after-xmlXIncludeNewRef.patch",
        "backport-xpath-Ignore-entity-ref-nodes-when-computing-node-ha.patch",
        "backport-SAX-Always-initialize-SAX1-element-handlers.patch",
        "Fix-malloc-fail.patch",
        "Fix-CVE-2024-34459.patch",
        "Fix-CVE-2024-56171.patch",
        "Fix-CVE-2025-24928.patch",
        "Fix-CVE-2025-27113.patch",
        "Fix-type-confusion-in-xmlSchemaCheckAGPropsCorrect.patch",
        "Fix-CVE-2019-19956.patch",
        "Fix-CVE-2025-32414.patch",
        "Fix-CVE-2025-32415.patch",
        "Backport-CVE-2025-6021-tree-Fix-integer-overflow-in-xmlBuildQName-c.patch",
        "Fix-relaxng-is-parsed-to-an-infinite-attrs-next-loop.patch",
        "Backport-CVE-2025-6170-Fix-potential-buffer-overflow-of-interactive-shell.patch",
        "Fix-CVE-2025-49794-CVE-2025-49796-memory-safety-issues-in-xmlSchematronReportOutput.patch",
        "Fix-CVE-2026-0990-catalog-prevent-inf-recursion-in-xmlCatalogXMLResolveURI.patch",
        "Fix-CVE-2026-0992-catalog-Ignore-repeated-nextCatalog-entries.patch",
        "Fix-CVE-2026-0989-Add-RelaxNG-include-limit.patch"
    ]

    for patch in patch_file:
        file_path = os.path.join(args.source_file, patch)
        apply_patch(file_path, target_dir)


def main():
    libpng_path = argparse.ArgumentParser()
    libpng_path.add_argument('--gen-dir', help='generate path of libxml2')
    libpng_path.add_argument('--source-file', help='libxml2 source compressed dir')
    args = libpng_path.parse_args()
    tar_file_path = os.path.join(args.source_file, "libxml2-2.9.14.tar.xz")
    target_dir = os.path.join(args.gen_dir, "libxml2-2.9.14")
    untar_file(tar_file_path, target_dir, args)
    do_patch(args, target_dir)
    return 0


if __name__ == '__main__':
    sys.exit(main())
