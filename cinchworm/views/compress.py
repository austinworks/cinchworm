import os
import uuid
import shutil
from pyramid.response import Response


def compress_binary(request):
    # ``filename`` contains the name of the file in string format.
    #
    # WARNING: this example does not deal with the fact that IE sends an
    # absolute file *path* as the filename.  This example is naive; it
    # trusts user input.

    filename = request.POST['binary_data'].filename

    # ``input_file`` contains the actual file data which needs to be
    # stored somewhere.

    input_file = request.POST['binary_data'].file

    # Note that we are generating our own filename instead of trusting
    # the incoming filename since that might result in insecure paths.
    # Please note that in a real application you would not use /tmp,
    # and if you write to an untrusted location you will need to do
    # some extra work to prevent symlink attacks.

    file_path = os.path.join('/tmp', '%s.mp3' % uuid.uuid4())

    # We first write to a temporary file to prevent incomplete files from
    # being used.

    temp_file_path = file_path + '~'

    # Finally write the data to a temporary file
    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    # Now that we know the file has been fully saved to disk move it into place.

    os.rename(temp_file_path, file_path)

    return Response('OK')
