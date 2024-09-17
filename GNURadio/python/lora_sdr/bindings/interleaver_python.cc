/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually
 * edited  */
/* The following lines can be configured to regenerate this file during cmake */
/* If manual edits are made, the following tags should be modified accordingly.
 */
/* BINDTOOL_GEN_AUTOMATIC(0) */
/* BINDTOOL_USE_PYGCCXML(0) */
/* BINDTOOL_HEADER_FILE(interleaver.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(e042ec01a2fc5bf489c2aa1a4fef7394) */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/lora_sdr/interleaver.h>
// pydoc.h is automatically generated in the build directory
#include <interleaver_pydoc.h>

void bind_interleaver(py::module &m) {

  using interleaver = ::gr::lora_sdr::interleaver;

  py::class_<interleaver, gr::block, gr::basic_block,
             std::shared_ptr<interleaver>>(m, "interleaver", D(interleaver))

      .def(py::init(&interleaver::make), py::arg("cr"), py::arg("sf"),
           py::arg("ldro"), py::arg("bw"), D(interleaver, make))

      .def("set_cr", &interleaver::set_cr, py::arg("cr"),
           D(interleaver, set_cr))

      .def("get_cr", &interleaver::get_cr, D(interleaver, get_cr))

      .def("set_sf", &interleaver::set_sf, py::arg("sf"),
           D(interleaver, set_sf))

      ;
}
