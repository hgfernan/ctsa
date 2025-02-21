# SPDX-License-Identifier: BSD-3-Clause

# TODO add the header files via a `target_include_directories`
add_executable(ctsa_ar_p0001_d0001 
			   ctsa_ar_p0001_d0001.c 
			   auxlib.c 
			   auxlib.h 
			   csv_in.c 
			   csv_in.h
			   sjson_macros.h
			   )

# TODO add the header files via a `target_include_directories`
add_executable(ctsa_ar_p0001_d0002 
			   ctsa_ar_p0001_d0002.c 
			   auxlib.c 
			   auxlib.h 
			   csv_in.c 
			   csv_in.h
			   sjson_macros.h
			   )
# TODO add the header files via a `target_include_directories`
add_executable(ctsa_ar_p0001_d0003 
			   ctsa_ar_p0001_d0003.c 
			   auxlib.c 
			   auxlib.h 
			   csv_in.c 
			   csv_in.h
			   sjson_macros.h
			   )

target_link_libraries(ctsa_ar_p0001_d0001 ctsalib m)
target_link_libraries(ctsa_ar_p0001_d0002 ctsalib m)
target_link_libraries(ctsa_ar_p0001_d0003 ctsalib m)

set_target_properties(ctsa_ar_p0001_d0001 ctsa_ar_p0001_d0002  ctsa_ar_p0001_d0003  
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${EXECUTABLE_OUTPUT_PATH}/ctsa"
)
