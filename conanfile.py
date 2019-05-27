# -*- coding: utf-8 -*-

from conans import CMake, ConanFile, tools
import os


class VulkanHppConan(ConanFile):
    name = "vulkan_hpp"
    version = "1.1.107"
    license = "Apache-2.0"
    author = "bincrafters <bincrafters@gmail.com>"
    url = "https://github.com/bincrafters-conan-vulkan_hpp"
    homepage = "https://github.com/KhronosGroup/Vulkan-Hpp"
    description = "Open-Source Vulkan C++ API"
    topics = ("vulkan", "khronos", "ghraphics", "api", "c++", )
    exports = ["LICENSE.md", ]

    _source_subfolder = "source_subfolder"
    _generator_git_revision = "7900c655f3e2be62fa8dd25e09eae1170c76cfa2"

    scm = {
        "type": "git",
        "url": "https://github.com/KhronosGroup/Vulkan-Hpp.git",
        "subfolder": _source_subfolder,
        "revision": _generator_git_revision,
    }

    generators = "cmake",

    def build_requirements(self):
        self.build_requires("tinyxml2/7.0.1@nicolastagliani/stable")

    def requirements(self):
        self.requires("vulkan_headers/{}@{}/{}".format(self.version, self.user, self.channel))

    def source(self):
        cmakelists = os.path.join(self._source_subfolder, "CMakeLists.txt")
        tools.replace_in_file(cmakelists,
                              "project(VulkanHppGenerator)",
                              "project(VulkanHppGenerator)\n"
                              "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n"
                              "conan_basic_setup(TARGETS)")

        tools.replace_in_file(cmakelists,
                              "${TINYXML2_SOURCES}",
                              "")
        tools.replace_in_file(cmakelists,
                              "${TINYXML2_HEADERS}",
                              "")
        tools.save_append(cmakelists, "\n\ntarget_link_libraries(VulkanHppGenerator PUBLIC CONAN_PKG::tinyxml2)\n")

        generator_src = os.path.join(self._source_subfolder, "VulkanHppGenerator.cpp")
        tools.replace_path_in_file(generator_src,
                                   "VULKAN_HPP_FILE",
                                   "destfilename")
        tools.replace_path_in_file(generator_src,
                                   "    std::string filename = (argc == 1) ? VK_SPEC : argv[1];",
                                   "    std::string filename = (argc < 2) ? VK_SPEC : argv[1];\n"
                                   "    std::string destfilename = (argc < 3) ? VULKAN_HPP_FILE : argv[2];")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=os.path.join(self.source_folder, self._source_subfolder))
        cmake.build()

        generator_exe = os.path.join(self.build_folder, "bin", "VulkanHppGenerator{}".format(".exe" if tools.os_info.is_windows else "",))
        vk_xml_path = os.path.join(self.deps_user_info["vulkan_headers"].VULKAN_REGISTRY_PATH, "vk.xml")
        vulkan_hpp_path = os.path.join(self.build_folder, "vulkan.hpp")
        self.run("{} {} {}".format(generator_exe, vk_xml_path, vulkan_hpp_path))

    def package(self):
        self.copy("vulkan.hpp", src=self.build_folder, dst=os.path.join("include", "vulkan"))
        self.copy("LICENSE.md", dst="licenses")
