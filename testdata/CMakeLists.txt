# SPDX-License-Identifier: BSD-3-Clause

# TODO add the header files via a `target_include_directories`
add_executable(artest_templ 
			   artest_templ.c 
			   auxlib.c 
			   auxlib.h 
			   csv_in.c 
			   csv_in.h 
			   )

target_link_libraries(artest_templ ctsalib m)

set_target_properties(artest_templ
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${EXECUTABLE_OUTPUT_PATH}"
)
