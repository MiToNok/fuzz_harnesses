In the following we list some crashed created by Atheris:

==aiohttp multipart== 
- TypeError: BodyPartReader._ init_() got an unexpected keyword argument ''_newline''
- affected at: Version 3.8.1
- Source: oss_fuzz/aiohttp/fuzz_multipart.py

==aiohttp webrequest== 
- UnicodeEncodeError: 'utf-8' codec can't encode characters in position 8-16: surrogates not allowed
Report:
- //[\000\011\000\000\000\000\000\377:.\000\000\000\000\377\000::\000\000\000\000\377:.\000\000\000\000\377%//[\331\331\331\331\331\331\331\331\331\331\331\331\331\331\331\336\331\331\377\000\000\000\000\000\000::\000\000\000\000\000\331\366\377\377:\000\000\000b\200\204:.\000\000\000\221..ppp]\003\032/\377\375pp\000\000
- Base64: JS8vWwAJAAAAAAD/Oi4AAAAA/wA6OgAAAAD/Oi4AAAAA/yUvL1vZ2dnZ2dnZ2dnZ2dnZ2dne2dn/AAAAAAAAOjoAAAAAANn2//86AAAAYoCEOi4AAACRLi5wcHBdAxov//1wcAAA
- affected at: Version 3.10
- Source: oss_fuzz/aiohttp/fuzz_web_request.py

==aiohttp payload url== 
- IndexError: string index out of range
Report:
- [//[]//\271
- affected at: Version 3.10
- Source: oss_fuzz/aiohttp/fuzz_payload_url.py