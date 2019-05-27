#include <vulkan/vulkan.hpp>
#include <iostream>

static char const* AppName = "01_InitInstance";
static char const* EngineName = "Vulkan.hpp";

int main()
{
  try
  {
    vk::ApplicationInfo applicationInfo(AppName, 1, EngineName, 1, VK_API_VERSION_1_1);
    vk::InstanceCreateInfo instanceCreateInfo({}, &applicationInfo);
    vk::UniqueInstance instance = vk::createInstanceUnique(instanceCreateInfo);
  }
  catch (vk::SystemError err)
  {
    std::cout << "vk::SystemError: " << err.what() << std::endl;
    exit(-1);
  }
  catch (...)
  {
    std::cout << "unknown error\n";
    exit(-1);
  }

  return 0;
}
