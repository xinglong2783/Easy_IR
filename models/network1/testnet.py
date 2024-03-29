import torch.nn as nn

# EDSR model
class EDSR(nn.Module):
    def __init__(self, in_ch, scale_factor, hide_dim=64):
        super(EDSR, self).__init__()
        self.conv1 = nn.Conv2d(in_ch, hide_dim, kernel_size=3, padding=1)
        self.res_blocks = nn.Sequential(*[ResidualBlock(hide_dim, hide_dim) for _ in range(16)])
        self.conv2 = nn.Conv2d(hide_dim, hide_dim, kernel_size=3, padding=1)
        self.upscale = nn.Identity()
        self.conv3 = nn.Conv2d(hide_dim, in_ch, kernel_size=3, padding=1)

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.res_blocks(x1)
        x3 = self.conv2(x2)
        x4 = x1 + x3
        x5 = self.upscale(x4)
        x6 = self.conv3(x5)
        return x6 + x

# Residual block
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)
        out += identity
        return out

def get_net(net_params):
    in_ch = net_params.get('in_ch', 1)
    scale_factor = net_params.get('scale_factor', 1)
    hide_dim = net_params.get('hide_dim', 32)
    return EDSR(in_ch, scale_factor, hide_dim)

if __name__ == "__main__":
    from torchsummary import summary
    net_params = {
        'in_ch': 1,
        'scale_factor': 2,
        'hide_dim': 32,
    }
    net = get_net(net_params)
    summary(net, (1, 256, 256), device='cpu')