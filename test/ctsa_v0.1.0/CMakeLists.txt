# SPDX-License-Identifier: BSD-3-Clause

# Collect all test source files
file(GLOB TEST_SOURCES "./ctsa_ar_p0001_d*.c")

# Function to add a test executable
function(add_test_executable test_source)
    get_filename_component(test_name ${test_source} NAME_WE)
	message(WARNING "source " ${test_source})
	message(WARNING "target " ${test_name})
    
    add_executable(${test_name} 
				   ${test_source}
				   auxlib.c 
				   auxlib.h 
				   csv_in.c 
				   csv_in.h
				   sjson_macros.h
				  )
    target_link_libraries(${test_name} ctsalib m)
    set_target_properties(${test_name}
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${EXECUTABLE_OUTPUT_PATH}/ctsa"
	)
endfunction()

# Generate executables for all tests
foreach(test_source ${TEST_SOURCES})
    add_test_executable(${test_source})
endforeach()
