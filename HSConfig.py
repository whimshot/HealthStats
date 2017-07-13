"""Configuration parser module for HealthStats."""
import ConfigParser


config = ConfigParser.ConfigParser()
config.readfp(open('HealthStats.conf'))
