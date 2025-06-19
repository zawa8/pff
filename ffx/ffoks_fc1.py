from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

profile_path = "/home/viml/.mozilla/firefox/profiles.ini"
profile = webdriver.FirefoxProfile(profile_path)

# Create Firefox options object
options = Options()
options.profile = profile

# Set font preferences
profile.set_preference("font.default.x-western", "serif") # Set default font to serif
profile.set_preference("font.name.serif.x-western", "hindienglosoftw8utf") # Set serif font to Times New Roman
profile.set_preference("font.size.variable.x-western", 16) # Set default font size to 16

############
#browser.display
############
profile.set_preference("browser.display.font.family", "hindienglosoftw8utf")  # Default font family
profile.set_preference("browser.display.font.size.proportional", 16)  # Font size for proportional text
profile.set_preference("browser.display.font.size.serif", 16)  # Font size for serif text
profile.set_preference("browser.display.font.size.sans_serif", 16)  # Font size for sans-serif text
profile.set_preference("browser.display.font.size.fixed", 16)  # Font size for fixed-width text
profile.set_preference("browser.display.font.size.monospace", 16)  # Font size for monospace text

# Advanced font settings
profile.set_preference("font.minimum", 16)  # Minimum font size
profile.set_preference("font.fallback", "hindienglosoftw8utf") # Fallback font
profile.set_preference("font.fallback.latin", "hindienglosoftw8utf") # Fallback font for Latin scripts
profile.set_preference("font.fallback.greek", "hindienglosoftw8utf") # Fallback font for Greek scripts

# devanagari
profile.set_preference("font.name.serif.x-devanagari", "Mangal")
profile.set_preference("font.name.sans-serif.x-devanagari", "Mangal")
profile.set_preference("font.name.monospace.x-devanagari", "Mangal")


# Disable page-specific fonts
profile.set_preference("font.allow_pages_to_choose_fonts", False)
############
############



# Initialize the WebDriver with the profile and options
driver = webdriver.Firefox(options=options)

# Now you can use the 'driver' object to interact with the browser
driver.get("https://www.example.com")

# Close the browser when done
driver.quit()
