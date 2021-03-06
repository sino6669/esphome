import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import lcd_base
from esphome.const import CONF_DATA_PINS, CONF_ENABLE_PIN, CONF_RS_PIN, CONF_RW_PIN, CONF_ID

AUTO_LOAD = ['lcd_base']

lcd_gpio_ns = cg.esphome_ns.namespace('lcd_gpio')
GPIOLCDDisplay = lcd_gpio_ns.class_('GPIOLCDDisplay', lcd_base.LCDDisplay)


def validate_pin_length(value):
    if len(value) != 4 and len(value) != 8:
        raise cv.Invalid("LCD Displays can either operate in 4-pin or 8-pin mode,"
                         "not {}-pin mode".format(len(value)))
    return value


CONFIG_SCHEMA = lcd_base.LCD_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(GPIOLCDDisplay),
    cv.Required(CONF_DATA_PINS): cv.All([pins.gpio_output_pin_schema], validate_pin_length),
    cv.Required(CONF_ENABLE_PIN): pins.gpio_output_pin_schema,
    cv.Required(CONF_RS_PIN): pins.gpio_output_pin_schema,
    cv.Optional(CONF_RW_PIN): pins.gpio_output_pin_schema,
})


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield lcd_base.setup_lcd_display(var, config)
    pins_ = []
    for conf in config[CONF_DATA_PINS]:
        pins_.append((yield cg.gpio_pin_expression(conf)))
    cg.add(var.set_data_pins(*pins_))
    enable = yield cg.gpio_pin_expression(config[CONF_ENABLE_PIN])
    cg.add(var.set_enable_pin(enable))

    rs = yield cg.gpio_pin_expression(config[CONF_RS_PIN])
    cg.add(var.set_rs_pin(rs))

    if CONF_RW_PIN in config:
        rw = yield cg.gpio_pin_expression(config[CONF_RW_PIN])
        cg.add(var.set_rw_pin(rw))
