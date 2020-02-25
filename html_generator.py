def generate_row_from_job_data(JobDataModel):
    return f"""
            <tr>
                <td>
                    <h3 align="center">{JobDataModel.title}</h3>
                    <p align="center">Location:{JobDataModel.location}</p>
                    <p align="center"><span>Posting link:</span> <a href="{JobDataModel.link}">link</a></p>
                </td>
            </tr>
    """

def generate_rows_from_job_data_list(JobDataModels):
    return [generate_row_from_job_data(model) for model in JobDataModels]
