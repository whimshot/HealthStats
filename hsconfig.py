"""Configuration parser module for HealthStats."""
import configparser


config = configparser.ConfigParser()
config.readfp(open('healthstats.conf'))
