# custom resource name
resource_name :covidFeedback

# required properties
property :instance_name, String, name_property: true
property :port, Integer, required: true
property :username, String, required: true

# creates CovidFeedback application
action :create do

    # creating directory for our application
    directory "/FeedbackApp-#{new_resource.instance_name}" do
        recursive true
        action :create
    end

    # install initial requirements
    bash 'install_requirements' do
        code <<-EOH
        
        sudo yum install git -y
        sudo yum install -y python3
        sudo yum install python3-pip
        sudo yum install firewalld
        sudo systemctl enable firewalld
        EOH
    end

    # set-up project directory to clone the repository
    bash 'setup_directory' do
        code <<-EOH
        cd /
        sudo git clone https://github.com/developers-cosmos/COVID19-Feedback.git
        sudo mv COVID19-Feedback/* FeedbackApp-#{new_resource.instance_name}/
        sudo rm -r COVID19-Feedback/
        cd FeedbackApp-#{new_resource.instance_name}
        sudo chmod 755 data.json
        EOH
    end

    # install required packages
    bash 'python_packages' do
        code <<-EOH
        cd /FeedbackApp-#{new_resource.instance_name}
        sudo pip3 install -r requirements.txt
        EOH
    end

    # opening the given port
    bash 'open_port' do
        code <<-EOH
        sudo firewall-cmd --zone=public --add-port=#{new_resource.port}/tcp --permanent
        sudo firewall-cmd --reload
        EOH
    end

    # creating a service our application
    template "/etc/systemd/system/FeedbackApp-#{new_resource.instance_name}.service" do
        source 'myservice.service.erb'
        variables(
          username: new_resource.username,
          instance_name: new_resource.instance_name,
          port: new_resource.port
        )
        action :create
    end

    # starting a service
    service "FeedbackApp-#{new_resource.instance_name}" do
        action [:start]
    end
end

# stop the CovidFeedback service
action :delete do
    service "FeedbackApp-#{new_resource.instance_name}" do
        action [:stop]
    end
end