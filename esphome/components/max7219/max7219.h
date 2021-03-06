#pragma once

#include "esphome/core/component.h"
#include "esphome/core/defines.h"

#ifdef USE_TIME
#include "esphome/components/time/real_time_clock.h"
#endif

#include "esphome/components/spi/spi.h"

namespace esphome {
namespace max7219 {

class MAX7219Component;

using max7219_writer_t = std::function<void(MAX7219Component &)>;

class MAX7219Component : public PollingComponent, public spi::SPIDevice {
 public:
  void set_writer(max7219_writer_t &&writer);

  void setup() override;

  void dump_config() override;

  void update() override;

  float get_setup_priority() const override;

  void display();

  void set_intensity(uint8_t intensity);
  void set_num_chips(uint8_t num_chips);

  /// Evaluate the printf-format and print the result at the given position.
  uint8_t printf(uint8_t pos, const char *format, ...) __attribute__((format(printf, 3, 4)));
  /// Evaluate the printf-format and print the result at position 0.
  uint8_t printf(const char *format, ...) __attribute__((format(printf, 2, 3)));

  /// Print `str` at the given position.
  uint8_t print(uint8_t pos, const char *str);
  /// Print `str` at position 0.
  uint8_t print(const char *str);

#ifdef USE_TIME
  /// Evaluate the strftime-format and print the result at the given position.
  uint8_t strftime(uint8_t pos, const char *format, time::ESPTime time) __attribute__((format(strftime, 3, 0)));

  /// Evaluate the strftime-format and print the result at position 0.
  uint8_t strftime(const char *format, time::ESPTime time) __attribute__((format(strftime, 2, 0)));
#endif

 protected:
  void send_byte_(uint8_t a_register, uint8_t data);
  void send_to_all_(uint8_t a_register, uint8_t data);
  bool is_device_msb_first() override;

  uint8_t intensity_{15};  /// Intensity of the display from 0 to 15 (most)
  uint8_t num_chips_{1};
  uint8_t *buffer_;
  optional<max7219_writer_t> writer_{};
};

}  // namespace max7219
}  // namespace esphome
