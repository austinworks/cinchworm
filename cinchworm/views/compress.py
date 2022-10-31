import os
import uuid
import shutil
from construct import Array, Int24sb, Struct
from pyramid.response import Response
from pyramid.view import view_config
from cinchworm import segmenter as seg


@view_config(route_name='compress')
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

    file_path = os.path.join(os.getcwd(), 'uploads', '%s.bin' % uuid.uuid4())

    # We first write to a temporary file to prevent incomplete files from
    # being used.

    temp_file_path = file_path + '~'

    # Finally write the data to a temporary file
    input_file.seek(0, os.SEEK_END)
    input_file_size = input_file.tell()
    input_file.seek(0)
    value_count = int(input_file_size / 3)
    format = Struct("data" / Array(value_count, Int24sb))
    container = format.parse(input_file.read())
    cleandata = [int(d) for d in container.data]
    segments = seg.Segmenter(cleandata).segments()

    with open(temp_file_path, 'wb') as output_file:
        for s in segments:
            output_file.write(s.emit())

    # Now that we know the file has been fully saved to disk move it into place.

    os.rename(temp_file_path, file_path)

    return Response('OK')
