import alteia



sdk = alteia.SDK(config_path='./config-connections.json')


analytic = sdk.analytics.search(name="alteiademo/pc2ph")[0]
sdk.analytics.delete(analytic=analytic.id)

sdk.analytics.create(name="alteiademo/pc2ph",
	version="1.0.0",
	display_name="Point Cloud to Plant Height",
	description="Converts a Point Cloud (.las) to a Plant Height (.tif)",
	docker_image="registry-1.docker.io/michaeldelagarde/pc2ph:latest",
	company="5c1a2567b3c575583e8a650d",
	instance_type='small',
	volume_size=20,
	inputs=[{
		"name": "input_pc",
		"display_name": "input_pc",
		"description": "Point Cloud (.las)",
		"scheme": {
			"type": "string", "pattern": "^[0-9a-f]{24}$"
		},
		"source": {
			"service": "data-manager",
			"resource": "dataset",
			"scheme": {
				"type": "object",
				"properties": {"type": {"const": "pcl"}},
				"required": ["type"]
			},
		},
		"required": True
	}],
	parameters=[{
		"name": "grid_size",
		"display_name": "grid_size",
		"description": "grid_size",
		"required": True,
		"scheme": {
			"type": "string"#, "pattern": "^[0-9]$"
		}
	 }],
	deliverables=[
	# {
	# 	"name": "outputtif",
	# 	"display_name": "outputtif",
	# 	"description": "outputtif",
	# 	"scheme": {
	# 		"type": "string", "pattern": "^[0-9a-f]{24}$"
	# 	},
	# 	"source": {
	# 		"service": "data-manager",
	# 		"resource": "dataset",
	# 		"scheme": {
	# 			"type": "object",
	# 			"properties": {"type": {"const": "raster"}},
	# 			"required": ["type"]
	# 		},
	# 	},
	# 	"required": False
	# }
	],
	tags=["croquette"],
	groups=["UTILS"])