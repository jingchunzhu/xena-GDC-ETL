import gdc
import string

projects_id = []
projects_name ={}
disease_code ={}
program_code ={}
output = "GDC-PANCAN/Xena_Matrices/GDC-PANCAN.project_info.tsv"

def project_info():
	#r = gdc.search('analysis/survival',
    #    in_filter={'project.project_id': self.projects},
    #    typ='json')['results'][0]['donors']

	r = gdc.search('projects',
        #in_filter={'project.project_id': self.projects},
        typ='json')
	
	for project in r:
		if project["id"] not in projects_id:
			projects_id.append(project["id"])
			projects_name [project["id"]] = project["name"]
			disease_code [project["id"]] = string.split(project["id"],"-")[1]
			program_code [project["id"]] = string.split(project["id"],"-")[0]

	return projects_id, projects_name, disease_code, program_code

def TCGA_TARGET_projects(projects_id):
	for project in projects_id:
		if string.find(project, "TCGA") != 0 and string.find(project, "TARGET") != 0:
			projects_id.remove(project)
	return projects_id

def download(projects_id):
	fout = open(output,'w')
	fout.write(string.join(['sample', "disease_code.project", "program_code.project"],'\t'))
	fout.write('\n')
	# all cases in a project
	for project_id in projects_id:
		r = gdc.search('cases',
	        in_filter={'project.project_id': project_id},
	        typ='json')

		print project_id
		for case in r:
			if case.has_key("submitter_sample_ids"):
				for sample in case["submitter_sample_ids"]:
					fout.write(string.join([sample, disease_code[project_id], program_code[project_id]],'\t'))
					fout.write('\n')
	fout.close()

projects_id, projects_name, disease_code, program_code = project_info()
projects_id = TCGA_TARGET_projects(projects_id)
download(projects_id)
