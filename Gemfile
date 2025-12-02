source "https://rubygems.org"

# Fix Ruby 3.4+ require issues: base64/logger/rexml are no longer auto-loaded
gem "base64"
gem "logger"
gem "rexml"

# Jekyll core
gem "jekyll", "~> 4.3"

# Modern Sass replacement (officially recommended)
gem "sass-embedded"

# Plugins
group :jekyll_plugins do
  gem "jekyll-email-protect"
end

# Windows-specific dependencies
gem "tzinfo-data", platforms: [:mingw, :mswin, :x64_mingw, :jruby]
gem "wdm", "~> 0.2" if Gem.win_platform?
gem "webrick", "~> 1.7"
gem "kramdown-parser-gfm"