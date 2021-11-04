import pulumi


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        outputs = args.inputs
        if args.typ == "docker:image:Image":
            outputs = {
                **args.inputs,
                "id": "test-string-1",
                "base_image_name": "test-me-1",
                "registry_server": "fake-it-1"
            }
        elif args.typ == "docker:remoteimage:RemoteImage":
            outputs = {
                **args.inputs,
                "id": "test-string-2",
                "repo_digest": f'{args.inputs.get("name")}'
            }
        else:
            outputs = args.inputs
        return [args.name + '_id', outputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        if args.token == "docker:getRegistryImage:getRegistryImage":
            return {
                "id": "registry-test-1",
                "name": "test-docker-1",
                "sha256_digest": "630794A13A82BC7B57BE8F743070B517CFD588D7258FCBADA1704B2FD69AD022",  # 'test-docker-1'
            }
        # if args.token == "docker:getRemoteImage:getRemoteImage":
        #     return {
        #
        #     }
        return {}


pulumi.runtime.set_mocks(MyMocks())

pulumi.runtime.set_all_config({
    "project:backend_port": "3000",
    "project:database": "cart",
    "project:frontend_port": "3001",
    "project:mongo_host": "mongodb://mongo:27017",
    "project:mongo_port": "27017",
    "project:node_environment": "development"
})

import my_docker


@pulumi.runtime.test
def test_docker_image():
    # super basic test just to run *something*
    def check_image_name(args):
        image_name = args
        assert 'mongo:bionic' in image_name, "must use bionic"

    return pulumi.Output.all(my_docker.mongo_image.name).apply(check_image_name)
