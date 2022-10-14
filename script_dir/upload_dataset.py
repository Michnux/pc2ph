import alteia



def upload_dataset(file_path, project_id, mission_id, script_dir):

	url = os.getenv("ALTEIA_PLATEFORM_URL")
	client_id = os.getenv("ALTEIA_CLIENT_ID")
	client_secret = os.getenv("ALTEIA_CLIENT_SECRET")
	if not url or not client_id or not client_secret:
		print('Plateform URL, client id or client secret not set')
		return

	sdk = alteia.SDK(
		url=url,
		client_id=client_id,
		client_secret=client_secret,
		connection={'disable_ssl_certificate': True},
	)


	new_dataset = sdk.datasets.create_raster_dataset(	name='output_plantheight',
														project=project_id,
														mission=mission_id,
														categories=['vegetation heights'])

	sdk.datasets.upload_file(dataset=new_dataset.id,
							 component='raster',
							 file_path=file_path)


if __name__ == "__main__":

	upload_dataset('../work_dir/output.tif', '61c1d5a73e614e00085c6a01', '61c4aeffd730570008b5e7c9', './')