#
# Cookbook Name:: CovidFeedback Application
# Recipe:: application
#
# Copyright (c) 2020 The Authors, All Rights Reserved.

# property: port is mandatory, make sure the given port is free
# property: username is mandatory
# default action :create


covidFeedback 'version1' do
    port 5005
    username "bunnyrb4"
end
