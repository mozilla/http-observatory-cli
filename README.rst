Mozilla HTTP Observatory :: Command Line Utility
================================================

Please note that this version of the Observatory CLI has been deprecated, and replaced with a `considerably more powerful version <https://github.com/mozilla/observatory-cli>`_.

Getting started with the HTTP Observatory (docker)
-----------------------------------------


.. code:: bash

    $ docker run --rm fgribreau/httpobs-cli www.mozilla.org
    Score: 30 [E]
    Modifiers:
        [  -5] Initial redirection from http to https is to a different host, preventing HSTS
        [  -5] Subresource Integrity (SRI) not implemented, but all external scripts are loaded over https
        [  -5] X-Content-Type-Options header not implemented
        [ -10] X-XSS-Protection header not implemented
        [ -20] HTTP Strict Transport Security (HSTS) header not implemented
        [ -25] Content Security Policy (CSP) header not implemented

Getting started with the HTTP Observatory (python)
-----------------------------------------

First install the client:

pip install httpobs-cli


.. code:: bash

    $ pip install httpobs-cli

And then scan websites to your heart's content, using our hosted
service:

::

    $ httpobs www.mozilla.org
    Score: 30 [E]
    Modifiers:
        [  -5] Initial redirection from http to https is to a different host, preventing HSTS
        [  -5] Subresource Integrity (SRI) not implemented, but all external scripts are loaded over https
        [  -5] X-Content-Type-Options header not implemented
        [ -10] X-XSS-Protection header not implemented
        [ -20] HTTP Strict Transport Security (HSTS) header not implemented
        [ -25] Content Security Policy (CSP) header not implemented

    $ httpobs www.google.com
    Score: 35 [D-]
    Modifiers:
        [  +5] Preloaded via the HTTP Public Key Pinning (HPKP) preloading process
        [  -5] X-Content-Type-Options header not implemented
        [ -20] Cookies set without using the Secure flag or set over http
        [ -20] HTTP Strict Transport Security (HSTS) header not implemented
        [ -25] Content Security Policy (CSP) header not implemented

    $ httpobs --zero github.com
    Score: 120 [A+]
    Modifiers:
        [  +5] HTTP Public Key Pinning (HPKP) header set to a minimum of 15 days (1296000)
        [  +5] Preloaded via the HTTP Strict Transport Security (HSTS) preloading process
        [  +5] Subresource Integrity (SRI) is implemented and all scripts are loaded from a similar origin
        [  +5] X-Frame-Options (XFO) implemented via the CSP frame-ancestors directive
        [   0] All cookies use the Secure flag and all session cookies use the HttpOnly flag
        [   0] Content Security Policy (CSP) implemented with 'unsafe-inline' inside style-src
        [   0] Content is not visible via cross-origin resource sharing (CORS) files or headers
        [   0] Contribute.json isn't required on websites that don't belong to Mozilla
        [   0] Initial redirection is to https on same host, final destination is https
        [   0] X-Content-Type-Options header set to "nosniff"
        [   0] X-XSS-Protection header set to "1; mode=block"

If you want additional options, such as to see the raw scan output, use
``httpobs --help``:

::

    $ httpobs --help
    usage: httpobs [options] host

    positional arguments:
      host           hostname of the website to scan

    optional arguments:
      -h, --help     show this help message and exit
      -d, --debug    output only raw JSON from scan and tests
      -r, --rescan   initiate a rescan instead of showing recent scan results
      -v, --verbose  display progress indicator
      -x, --hidden   don't list scan in the recent scan results
      -z, --zero     show test results that don't affect the final score

Authors
-------

-  April King

License
-------

-  Mozilla Public License Version 2.0
