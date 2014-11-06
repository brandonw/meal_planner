Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/trusty64'

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 80

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provisioning/site.yml"
        ansible.verbose = true
    end
end